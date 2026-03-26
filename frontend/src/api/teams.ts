import { apiRequest } from "./client";
import type { Team, TeamMembership } from "../types";

export interface GenerateTeamsPayload {
  names: string[];
}

export interface TeamHistoryResponse {
  team: Team;
  memberships: TeamMembership[];
  stats: {
    wins: number;
    draws: number;
    losses: number;
    goals_for: number;
    goals_against: number;
    total_matches: number;
  };
}

export interface TeamsResponse {
  owned_teams: Team[];
  member_teams: Team[];
}

export function generateTeams(payload: GenerateTeamsPayload): Promise<TeamsResponse> {
  return apiRequest<TeamsResponse>("/teams/generate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function listTeams(): Promise<TeamsResponse> {
  return apiRequest<TeamsResponse>("/teams");
}

export function getTeamHistory(teamId: number): Promise<TeamHistoryResponse> {
  return apiRequest<TeamHistoryResponse>(`/teams/${teamId}/history`);
}
