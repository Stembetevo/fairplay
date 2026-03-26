import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listMatches } from "../api/matches";
import type { Match } from "../types";

export function MatchesPage() {
  const [upcoming, setUpcoming] = useState<Match[]>([]);
  const [played, setPlayed] = useState<Match[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadMatches();
  }, []);

  async function loadMatches() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listMatches();
      setUpcoming(data.upcoming_matches);
      setPlayed(data.played_matches);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load matches");
    } finally {
      setIsLoading(false);
    }
  }

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="stack">
      <h2>Matches</h2>

      <Link to="/matches/new">
        <button>Create Match</button>
      </Link>

      {error && <p className="error">{error}</p>}

      {upcoming.length > 0 && (
        <section>
          <h3>Upcoming Matches</h3>
          <div className="matches-grid">
            {upcoming.map((match) => (
              <div key={match.id} className="card">
                <p className="match-header">
                  {match.team_A.name} vs {match.team_B.name}
                </p>
                <p>Status: {match.status}</p>
                {match.played_at && (
                  <p>Scheduled: {new Date(match.played_at).toLocaleDateString()}</p>
                )}
                {match.location && <p>Location: {match.location}</p>}
                <Link to={`/matches/${match.id}`}>
                  <button>View Details</button>
                </Link>
              </div>
            ))}
          </div>
        </section>
      )}

      {played.length > 0 && (
        <section>
          <h3>Played Matches</h3>
          <div className="matches-grid">
            {played.map((match) => (
              <div key={match.id} className="card">
                <p className="match-result">
                  {match.team_A.name}
                  {match.score_a !== null ? ` ${match.score_a}` : " ?"}
                  {" - "}
                  {match.score_b !== null ? `${match.score_b} ` : "? "}
                  {match.team_B.name}
                </p>
                {match.location && <p>Location: {match.location}</p>}
                <Link to={`/matches/${match.id}`}>
                  <button>View Details</button>
                </Link>
              </div>
            ))}
          </div>
        </section>
      )}

      {upcoming.length === 0 && played.length === 0 && (
        <p>No matches yet. Create one to get started!</p>
      )}
    </div>
  );
}
