import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listTeams } from "../api/teams";
import type { Team } from "../types";

export function TeamsPage() {
  const [ownedTeams, setOwnedTeams] = useState<Team[]>([]);
  const [memberTeams, setMemberTeams] = useState<Team[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTeams();
  }, []);

  async function loadTeams() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listTeams();
      setOwnedTeams(data.owned_teams);
      setMemberTeams(data.member_teams);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load teams");
    } finally {
      setIsLoading(false);
    }
  }

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="stack">
      <h2>Teams</h2>

      {error && <p className="error">{error}</p>}

      {ownedTeams.length === 0 && memberTeams.length === 0 ? (
        <div>
          <p>No teams yet.</p>
          <Link to="/teams/generate">
            <button>Generate Teams</button>
          </Link>
        </div>
      ) : (
        <>
          {ownedTeams.length > 0 && (
            <section>
              <h3>Your Teams</h3>
              <div className="teams-grid">
                {ownedTeams.map((team) => (
                  <div key={team.id} className="card">
                    <h4>{team.name}</h4>
                    <p>Players: {team.players.length}</p>
                    <p>Total Rating: {team.total_rating}</p>
                    <p>Avg Rating: {team.avg_rating.toFixed(1)}</p>
                    <Link to={`/teams/${team.id}/history`}>
                      <button>View History</button>
                    </Link>
                  </div>
                ))}
              </div>
            </section>
          )}

          {memberTeams.length > 0 && (
            <section>
              <h3>Teams You're In</h3>
              <div className="teams-grid">
                {memberTeams.map((team) => (
                  <div key={team.id} className="card">
                    <h4>{team.name}</h4>
                    <p>Owner: {team.owner_username}</p>
                    <p>Players: {team.players.length}</p>
                    <p>Total Rating: {team.total_rating}</p>
                    <p>Avg Rating: {team.avg_rating.toFixed(1)}</p>
                    <Link to={`/teams/${team.id}/history`}>
                      <button>View History</button>
                    </Link>
                  </div>
                ))}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}
