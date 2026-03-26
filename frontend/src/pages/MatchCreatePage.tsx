import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { createMatch } from "../api/matches";
import { listTeams } from "../api/teams";
import type { Team } from "../types";

export function MatchCreatePage() {
  const navigate = useNavigate();

  const [teams, setTeams] = useState<Team[]>([]);
  const [teamA, setTeamA] = useState<number | null>(null);
  const [teamB, setTeamB] = useState<number | null>(null);
  const [playedAt, setPlayedAt] = useState("");
  const [location, setLocation] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await listTeams();
        const allTeams = [...data.owned_teams, ...data.member_teams];
        setTeams(allTeams);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load teams");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, []);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);

    if (!teamA || !teamB) {
      setError("Please select both teams");
      return;
    }

    if (teamA === teamB) {
      setError("A team cannot play against itself");
      return;
    }

    setIsSubmitting(true);

    try {
      await createMatch({
        team_A: teamA,
        team_B: teamB,
        played_at: playedAt || undefined,
        location: location || undefined,
      });
      navigate("/matches");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create match");
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="stack">
      <h2>Create Match</h2>

      <form onSubmit={handleSubmit} className="card">
        <label>
          Team A
          <select value={teamA ?? ""} onChange={(e) => setTeamA(e.target.value ? parseInt(e.target.value) : null)} required>
            <option value="">Select Team A</option>
            {teams.map((team) => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Team B
          <select value={teamB ?? ""} onChange={(e) => setTeamB(e.target.value ? parseInt(e.target.value) : null)} required>
            <option value="">Select Team B</option>
            {teams.map((team) => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Scheduled Date & Time (optional)
          <input
            type="datetime-local"
            value={playedAt}
            onChange={(e) => setPlayedAt(e.target.value)}
          />
        </label>

        <label>
          Location (optional)
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Match venue"
          />
        </label>

        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Creating..." : "Create Match"}
        </button>
      </form>
    </div>
  );
}
