async function request(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...options,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }
  if (!response.ok) {
    const error = new Error((data && data.error) || "Something went wrong");
    error.status = response.status;
    throw error;
  }
  return data;
}

export const api = {
  me: () => request("/auth/me"),
  login: (body) => request("/auth/login", { method: "POST", body }),
  register: (body) => request("/auth/register", { method: "POST", body }),
  logout: () => request("/auth/logout", { method: "POST" }),
  topics: () => request("/topics"),
  startQuiz: (topicId) => request(`/quiz/${topicId}`),
  submitQuiz: (topicId, answers) =>
    request(`/quiz/${topicId}/submit`, { method: "POST", body: { answers } }),
  attempt: (id) => request(`/attempts/${id}`),
  dashboard: () => request("/dashboard"),
  analytics: () => request("/analytics"),
  achievements: () => request("/achievements"),
};
