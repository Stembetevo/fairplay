import { useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { generateTeams } from "../api/teams";

export function TeamGeneratePage() {
  const navigate = useNavigate();

  const [numTeams, setNumTeams] = useState(2);
  const [teamNames, setTeamNames] = useState<string[]>(["Team A", "Team B"]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function updateTeamName(index: number, value: string) {
    const updated = [...teamNames];
    updated[index] = value;
    setTeamNames(updated);
  }

  function updateNumTeams(newNum: number) {
    setNumTeams(newNum);
    const updated = teamNames.slice(0, newNum);
    while (updated.length < newNum) {
      updated.push(`Team ${String.fromCharCode(65 + updated.length)}`);
    }
    setTeamNames(updated);
  }

  async function handleGenerate(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const validNames = teamNames.filter((name) => name.trim());
      if (validNames.length === 0) {
        setError("Please enter at least one team name");
        return;
      }

      await generateTeams({ names: validNames });
      navigate("/teams");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate teams");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="stack">
      <h2>Generate Teams</h2>
      <p>Use the snake draft algorithm to create balanced teams from your players.</p>

      <form onSubmit={handleGenerate} className="card">
        <label>
          Number of Teams (2-10)
          <input
            type="number"
            min={2}
            max={10}
            value={numTeams}
            onChange={(e) => updateNumTeams(Math.max(2, Math.min(10, parseInt(e.target.value))))}
          />
        </label>

        <div className="stack">
          <h3>Team Names</h3>
          {teamNames.map((name, i) => (
            <label key={i}>
              Team {i + 1} Name
              <input
                value={name}
                onChange={(e) => updateTeamName(i, e.target.value)}
                placeholder={`Team ${String.fromCharCode(65 + i)}`}
              />
            </label>
          ))}
        </div>

        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={isLoading}>
          {isLoading ? "Generating..." : "Generate Teams"}
        </button>
      </form>
    </div>
  );
}
