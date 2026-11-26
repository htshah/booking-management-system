// crypto.randomUUID() only exists in secure contexts (HTTPS or localhost),
// so fall back to a manual v4 UUID when served over plain HTTP.
function generateUUID() {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export function getUserId() {
  let userId = localStorage.getItem("rally_user_id");
  if (!userId) {
    userId = generateUUID();
    localStorage.setItem("rally_user_id", userId);
  }
  return userId;
}
