export function getUserId() {
  let userId = localStorage.getItem("rally_user_id");
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("rally_user_id", userId);
  }
  return userId;
}
