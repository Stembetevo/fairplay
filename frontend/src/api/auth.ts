import { apiRequest } from "./client";
import type { Position, UserSummary } from "../types";

export interface RegisterPayload {
  username: string;
  email: string;
  password1: string;
  preferred_position: Position;
}

export interface LoginPayload {
  username: string;
  password: string;
}

interface AvailableUsersResponse {
  usernames: string[];
}

export function getCurrentUser(): Promise<UserSummary | null> {
  return apiRequest<UserSummary | null>("/auth/me");
}

export async function listAvailableUsernames(): Promise<string[]> {
  const response = await apiRequest<AvailableUsersResponse>("/auth/users");
  return response.usernames;
}

export function registerUser(payload: RegisterPayload): Promise<UserSummary> {
  return apiRequest<UserSummary>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function loginUser(payload: LoginPayload): Promise<UserSummary> {
  return apiRequest<UserSummary>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function logoutUser(): Promise<void> {
  return apiRequest<void>("/auth/logout", {
    method: "POST",
  });
}
