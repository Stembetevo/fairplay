import { apiRequest } from "./client";
import type { Player, Position } from "../types";

export interface CreatePlayerPayload {
  username: string;
  position_override?: Position;
  rating?: number;
}

export interface UpdatePlayerPayload {
  position?: Position;
  rating?: number;
}

export function listPlayers(): Promise<Player[]> {
  return apiRequest<Player[]>("/players");
}

export function createPlayer(payload: CreatePlayerPayload): Promise<Player> {
  return apiRequest<Player>("/players", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updatePlayer(
  playerId: number,
  payload: UpdatePlayerPayload
): Promise<Player> {
  return apiRequest<Player>(`/players/${playerId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deletePlayer(playerId: number): Promise<void> {
  return apiRequest<void>(`/players/${playerId}`, {
    method: "DELETE",
  });
}

export function resetPlayers(): Promise<void> {
  return apiRequest<void>("/players/reset", {
    method: "POST",
  });
}
