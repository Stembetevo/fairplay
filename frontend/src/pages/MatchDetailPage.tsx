import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getMatch, recordMatchResult } from "../api/matches";
import type { MatchDetailResponse } from "../api/matches";

export function MatchDetailPage() {
  const { matchId } = useParams<{ matchId: string }>();
  const navigate = useNavigate();

  const [data, setData] = useState<MatchDetailResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showResultForm, setShowResultForm] = useState(false);
  const [scoreA, setScoreA] = useState("");
  const [scoreB, setScoreB] = useState("");
  const [status, setStatus] = useState<"Scheduled" | "Played" | "Cancelled">("Played");

  useEffect(() => {
    async function load() {
      if (!matchId) return;

      setIsLoading(true);
      setError(null);
      try {
        const result = await getMatch(parseInt(matchId));
        setData(result);
        setScoreA(result.match.score_a?.toString() ?? "");
        setScoreB(result.match.score_b?.toString() ?? "");
        setStatus(result.match.status);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load match");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, [matchId]);

  async function handleRecordResult(event: FormEvent) {
    event.preventDefault();
    if (!matchId || !data) return;

    try {
      await recordMatchResult(parseInt(matchId), {
        score_a: parseInt(scoreA),
        score_b: parseInt(scoreB),
        status,
      });

      setShowResultForm(false);
      // Reload match data
      const updated = await getMatch(parseInt(matchId));
      setData(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to record result");
    }
  }

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!data) return <div>Match not found</div>;

  const { match, team_a_participations, team_b_participations, can_edit } = data;

  return (
    <div className="stack">
      <button onClick={() => navigate("/matches")}>← Back to Matches</button>

      <h2>
        {match.team_A.name} vs {match.team_B.name}
      </h2>

      <section className="card">
        <h3>Match Result</h3>
        {match.score_a !== null && match.score_b !== null ? (
          <p className="match-result">
            {match.team_A.name} {match.score_a} - {match.score_b} {match.team_B.name}
          </p>
        ) : (
          <p>No result recorded yet</p>
        )}

        <p>Status: {match.status}</p>
        {match.played_at && (
          <p>Scheduled: {new Date(match.played_at).toLocaleDateString()}</p>
        )}
        {match.location && <p>Location: {match.location}</p>}

        {can_edit && !showResultForm && (
          <button onClick={() => setShowResultForm(true)}>Record Result</button>
        )}

        {can_edit && showResultForm && (
          <form onSubmit={handleRecordResult} className="stack">
            <label>
              {match.team_A.name} Goals
              <input
                type="number"
                min={0}
                value={scoreA}
                onChange={(e) => setScoreA(e.target.value)}
                required
              />
            </label>
            <label>
              {match.team_B.name} Goals
              <input
                type="number"
                min={0}
                value={scoreB}
                onChange={(e) => setScoreB(e.target.value)}
                required
              />
            </label>
            <label>
              Status
              <select value={status} onChange={(e) => setStatus(e.target.value as typeof status)}>
                <option value="Scheduled">Scheduled</option>
                <option value="Played">Played</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </label>
            <div className="button-group">
              <button type="submit">Save</button>
              <button type="button" onClick={() => setShowResultForm(false)}>
                Cancel
              </button>
            </div>
          </form>
        )}
      </section>

      <section>
        <h3>{match.team_A.name} Roster</h3>
        {team_a_participations.length === 0 ? (
          <p>No players</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Player</th>
                <th>Goals</th>
                <th>Assists</th>
                <th>Minutes</th>
                <th>Rating</th>
              </tr>
            </thead>
            <tbody>
              {team_a_participations.map((p) => (
                <tr key={p.id}>
                  <td>{p.username}</td>
                  <td>{p.goals}</td>
                  <td>{p.assists}</td>
                  <td>{p.minutes_played ?? "—"}</td>
                  <td>{p.match_rating ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section>
        <h3>{match.team_B.name} Roster</h3>
        {team_b_participations.length === 0 ? (
          <p>No players</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Player</th>
                <th>Goals</th>
                <th>Assists</th>
                <th>Minutes</th>
                <th>Rating</th>
              </tr>
            </thead>
            <tbody>
              {team_b_participations.map((p) => (
                <tr key={p.id}>
                  <td>{p.username}</td>
                  <td>{p.goals}</td>
                  <td>{p.assists}</td>
                  <td>{p.minutes_played ?? "—"}</td>
                  <td>{p.match_rating ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
