import { apiRequest } from "./client";
import type { Match, MatchParticipation } from "../types";

export interface CreateMatchPayload {
  team_A: number;
  team_B: number;
  played_at?: string;
  location?: string;
}

export interface MatchListResponse {
  upcoming_matches: Match[];
  played_matches: Match[];
}

export interface MatchDetailResponse {
  match: Match;
  team_a_participations: MatchParticipation[];
  team_b_participations: MatchParticipation[];
  can_edit: boolean;
}

export interface MatchResultPayload {
  score_a: number;
  score_b: number;
  status: "Scheduled" | "Played" | "Cancelled";
}

export function listMatches(): Promise<MatchListResponse> {
  return apiRequest<MatchListResponse>("/matches");
}

export function createMatch(payload: CreateMatchPayload): Promise<Match> {
  return apiRequest<Match>("/matches", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getMatch(matchId: number): Promise<MatchDetailResponse> {
  return apiRequest<MatchDetailResponse>(`/matches/${matchId}`);
}

export function recordMatchResult(
  matchId: number,
  payload: MatchResultPayload
): Promise<Match> {
  return apiRequest<Match>(`/matches/${matchId}/result`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}
