import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getTeamHistory } from "../api/teams";
import type { Team, TeamMembership } from "../types";

interface TeamHistoryData {
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

export function TeamHistoryPage() {
  const { teamId } = useParams<{ teamId: string }>();
  const navigate = useNavigate();

  const [data, setData] = useState<TeamHistoryData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      if (!teamId) return;

      setIsLoading(true);
      setError(null);
      try {
        const result = await getTeamHistory(parseInt(teamId));
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load team history");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, [teamId]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div className="error"> {error}</div>;
  if (!data) return <div>Team not found</div>;

  const { team, stats, memberships } = data;

  return (
    <div className="stack">
      <button onClick={() => navigate("/teams")}>← Back to Teams</button>

      <h2>{team.name}</h2>

      <section className="card">
        <h3>Team Stats</h3>
        <div className="stats-grid">
          <div>
            <p className="stat-value">{stats.total_matches}</p>
            <p className="stat-label">Matches</p>
          </div>
          <div>
            <p className="stat-value">{stats.wins}</p>
            <p className="stat-label">Wins</p>
          </div>
          <div>
            <p className="stat-value">{stats.draws}</p>
            <p className="stat-label">Draws</p>
          </div>
          <div>
            <p className="stat-value">{stats.losses}</p>
            <p className="stat-label">Losses</p>
          </div>
          <div>
            <p className="stat-value">{stats.goals_for}</p>
            <p className="stat-label">Goals For</p>
          </div>
          <div>
            <p className="stat-value">{stats.goals_against}</p>
            <p className="stat-label">Goals Against</p>
          </div>
        </div>
      </section>

      <section>
        <h3>Members</h3>
        {memberships.length === 0 ? (
          <p>No members</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Player</th>
                <th>Joined</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {memberships.map((m) => (
                <tr key={m.id}>
                  <td>{m.username}</td>
                  <td>{new Date(m.joined_at).toLocaleDateString()}</td>
                  <td>{m.left_at ? `Left ${new Date(m.left_at).toLocaleDateString()}` : "Current"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
