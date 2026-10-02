import AppKit
import ApplicationServices

func children(_ e: AXUIElement, _ attribute: String) -> [AXUIElement] {
  var v: CFTypeRef?
  guard AXUIElementCopyAttributeValue(e, attribute as CFString, &v) == .success else { return [] }
  if let a = v as? [AXUIElement] { return a }
  if let v = v, CFGetTypeID(v) == AXUIElementGetTypeID() {
    return [unsafeBitCast(v, to: AXUIElement.self)]
  }
  return []
}
func text(_ e: AXUIElement, _ attribute: String) -> String {
  var v: CFTypeRef?
  AXUIElementCopyAttributeValue(e, attribute as CFString, &v)
  return v as? String ?? ""
}
func walk(_ e: AXUIElement, depth: Int = 0) -> [AXUIElement] {
  if depth > 6 { return [] }
  return [e] + children(e, kAXChildrenAttribute).flatMap { walk($0, depth: depth + 1) }
}
func alert(_ message: String) -> Never {
  NSApplication.shared.setActivationPolicy(.regular)
  NSApplication.shared.activate(ignoringOtherApps: true)
  let a = NSAlert()
  a.messageText = "DDPM Launcher"
  a.informativeText = message
  a.addButton(withTitle: "OK")
  a.window.title = "DDPM Launcher"
  a.runModal()
  exit(1)
}
guard
  AXIsProcessTrustedWithOptions(
    [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true] as CFDictionary)
else {
  alert(
    "Enable DDPM Launcher in System Settings → Privacy & Security → Accessibility, then launch it again."
  )
}
if NSRunningApplication.runningApplications(withBundleIdentifier: "Qisda.DDPM").isEmpty {
  NSWorkspace.shared.open(URL(fileURLWithPath: "/Applications/DDPM/DDPM.app"))
  for _ in 0..<30 {
    if !NSRunningApplication.runningApplications(withBundleIdentifier: "Qisda.DDPM").isEmpty {
      break
    }
    Thread.sleep(forTimeInterval: 0.1)
  }
  Thread.sleep(forTimeInterval: 1)
}
guard let app = NSRunningApplication.runningApplications(withBundleIdentifier: "Qisda.DDPM").first
else { alert("Dell Display and Peripheral Manager could not start.") }
let root = AXUIElementCreateApplication(app.processIdentifier)
AXUIElementSetMessagingTimeout(root, 2)
func raiseControls() -> Bool {
  for w in children(root, kAXWindowsAttribute) where text(w, kAXTitleAttribute) == "DDPM" {
    if walk(w).contains(where: { text($0, kAXTitleAttribute) == "Brightness / Contrast" }) {
      app.activate(options: [])
      return AXUIElementPerformAction(w, kAXRaiseAction as CFString) == .success
    }
  }
  return false
}
func openItem() -> Bool {
  for e in walk(root) where text(e, kAXTitleAttribute) == "Open Dell Display and Peripheral Manager"
  {
    return AXUIElementPerformAction(e, kAXPressAction as CFString) == .success
  }
  return false
}
if raiseControls() { exit(0) }
let bars =
  children(root, kAXExtrasMenuBarAttribute)
  + children(root, kAXChildrenAttribute).filter { text($0, kAXRoleAttribute) == kAXMenuBarRole }
guard
  let icon = bars.flatMap({ walk($0) }).first(where: {
    text($0, kAXRoleAttribute) == kAXMenuBarItemRole && text($0, kAXTitleAttribute).isEmpty
  })
else { alert("Dell’s menu icon is unavailable. Restart DDPM and try again.") }
var pos: CFTypeRef?
var size: CFTypeRef?
AXUIElementCopyAttributeValue(icon, kAXPositionAttribute as CFString, &pos)
AXUIElementCopyAttributeValue(icon, kAXSizeAttribute as CFString, &size)
guard let pos = pos, let size = size else { alert("Dell’s menu icon location is unavailable.") }
var point = CGPoint.zero
var dimensions = CGSize.zero
AXValueGetValue(unsafeBitCast(pos, to: AXValue.self), .cgPoint, &point)
AXValueGetValue(unsafeBitCast(size, to: AXValue.self), .cgSize, &dimensions)
point.x += dimensions.width / 2
point.y += dimensions.height / 2
let previous = CGEvent(source: nil)?.location
CGEvent(
  mouseEventSource: nil, mouseType: .rightMouseDown, mouseCursorPosition: point, mouseButton: .right
)?.post(tap: .cghidEventTap)
CGEvent(
  mouseEventSource: nil, mouseType: .rightMouseUp, mouseCursorPosition: point, mouseButton: .right)?
  .post(tap: .cghidEventTap)
var selected = false
for _ in 0..<30 {
  Thread.sleep(forTimeInterval: 0.1)
  if openItem() {
    selected = true
    break
  }
}
if let previous = previous { CGWarpMouseCursorPosition(previous) }
if selected {
  for _ in 0..<40 {
    Thread.sleep(forTimeInterval: 0.1)
    if raiseControls() { exit(0) }
  }
}
alert("Dell did not open its controls. Restart DDPM and try again.")
