import { defineStore } from "pinia";
import request from "../utils/request";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access_token") || "",
    refreshToken: localStorage.getItem("refresh_token") || "",
    user: JSON.parse(localStorage.getItem("user") || "null"),
  }),
  actions: {
    /**
     * Execute username/password login flow and persist session.
     */
    async login(payload) {
      const res = await request.post("/auth/login", payload);
      this.accessToken = res.data.tokens.access;
      this.refreshToken = res.data.tokens.refresh;
      this.user = res.data.user;
      localStorage.setItem("access_token", this.accessToken);
      localStorage.setItem("refresh_token", this.refreshToken);
      localStorage.setItem("user", JSON.stringify(this.user));
    },
    /**
     * Clear local session and reset store state.
     */
    logout() {
      this.accessToken = "";
      this.refreshToken = "";
      this.user = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
    },
  },
});
