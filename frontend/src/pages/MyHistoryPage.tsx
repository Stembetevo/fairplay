import { useEffect, useState } from "react";
import { getMyHistory } from "../api/history";
import type { MyHistoryResponse } from "../types";

export function MyHistoryPage() {
  const [data, setData] = useState<MyHistoryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      setIsLoading(true);
      setError(null);
      try {
        const result = await getMyHistory();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load history");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, []);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!data) return <div>No history</div>;

  const { stats, participations, memberships } = data;

  return (
    <div className="stack">
      <h2>My History</h2>

      <section className="card">
        <h3>Personal Stats</h3>
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
            <p className="stat-value">{stats.goals}</p>
            <p className="stat-label">Goals</p>
          </div>
          <div>
            <p className="stat-value">{stats.assists}</p>
            <p className="stat-label">Assists</p>
          </div>
        </div>
      </section>

      {memberships.length > 0 && (
        <section>
          <h3>Team Memberships</h3>
          <table>
            <thead>
              <tr>
                <th>Team</th>
                <th>Joined</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {memberships.map((m) => (
                <tr key={m.id}>
                  <td>{m.team_name}</td>
                  <td>{new Date(m.joined_at).toLocaleDateString()}</td>
                  <td>
                    {m.left_at
                      ? `Left ${new Date(m.left_at).toLocaleDateString()}`
                      : "Current"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {participations.length > 0 && (
        <section>
          <h3>Match Participations</h3>
          <table>
            <thead>
              <tr>
                <th>Match</th>
                <th>Team</th>
                <th>Goals</th>
                <th>Assists</th>
                <th>Rating</th>
              </tr>
            </thead>
            <tbody>
              {participations.map((p) => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.team_name}</td>
                  <td>{p.goals}</td>
                  <td>{p.assists}</td>
                  <td>{p.match_rating ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {participations.length === 0 && memberships.length === 0 && (
        <p>No history yet. Participate in matches to build your history!</p>
      )}
    </div>
  );
}
