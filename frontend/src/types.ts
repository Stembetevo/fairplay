export type Position = "Striker" | "Defender" | "MidFielder" | "GoalKeeper";

export interface UserSummary {
  id: number;
  username: string;
  email?: string;
}

export interface Player {
  id: number;
  user_id: number;
  username: string;
  owner_id: number;
  position: Position;
  rating: number;
  team_id: number | null;
  team_name: string | null;
}

export interface Team {
  id: number;
  name: string;
  owner_id: number;
  owner_username: string;
  members_count?: number;
  total_rating: number;
  avg_rating: number;
  players: Player[];
}

export interface Match {
  id: number;
  team_A: Team;
  team_B: Team;
  status: "Scheduled" | "Played" | "Cancelled";
  played_at: string | null;
  location: string;
  score_a: number | null;
  score_b: number | null;
  winner_team_id: number | null;
}

export interface TeamMembership {
  id: number;
  team_id: number;
  team_name: string;
  player_id: number;
  username: string;
  joined_at: string;
  left_at: string | null;
}

export interface MatchParticipation {
  id: number;
  match_id: number;
  team_id: number;
  team_name: string;
  player_id: number;
  username: string;
  goals: number;
  assists: number;
  minutes_played: number | null;
  match_rating: number | null;
}

export interface MyHistoryResponse {
  memberships: TeamMembership[];
  participations: MatchParticipation[];
  stats: {
    total_matches: number;
    wins: number;
    draws: number;
    losses: number;
    goals: number;
    assists: number;
  };
}

export interface ApiError {
  detail?: string;
  message?: string;
  [key: string]: unknown;
}
