import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import {
  listPlayers,
  createPlayer,
  updatePlayer,
  deletePlayer,
  resetPlayers,
} from "../api/players";
import type { Player, Position } from "../types";

const positions: Position[] = ["Striker", "Defender", "MidFielder", "GoalKeeper"];

export function PlayersPage() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  const [formData, setFormData] = useState({
    username: "",
    position: "Striker" as Position,
    rating: 70,
  });

  useEffect(() => {
    loadPlayers();
  }, []);

  async function loadPlayers() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listPlayers();
      setPlayers(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load players");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleAddPlayer(event: FormEvent) {
    event.preventDefault();
    try {
      await createPlayer({
        username: formData.username,
        position_override: formData.position !== "Striker" ? formData.position : undefined,
        rating: formData.rating,
      });
      setFormData({ username: "", position: "Striker", rating: 70 });
      setShowAddForm(false);
      await loadPlayers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add player");
    }
  }

  async function handleUpdatePlayer(playerId: number, event: FormEvent) {
    event.preventDefault();
    try {
      await updatePlayer(playerId, {
        position: formData.position,
        rating: formData.rating,
      });
      setEditingId(null);
      setFormData({ username: "", position: "Striker", rating: 70 });
      await loadPlayers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update player");
    }
  }

  async function handleDeletePlayer(playerId: number) {
    if (!window.confirm("Are you sure you want to remove this player?")) return;

    try {
      await deletePlayer(playerId);
      await loadPlayers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete player");
    }
  }

  async function handleResetPlayers() {
    if (!window.confirm("This will remove ALL your players. Continue?")) return;

    try {
      await resetPlayers();
      await loadPlayers();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to reset players");
    }
  }

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="stack">
      <h2>Your Players</h2>

      <div className="controls">
        <button onClick={() => setShowAddForm(!showAddForm)}>
          {showAddForm ? "Cancel" : "Add Player"}
        </button>
        {players.length > 0 && (
          <button onClick={handleResetPlayers} className="danger">
            Reset All
          </button>
        )}
      </div>

      {error && <p className="error">{error}</p>}

      {showAddForm && (
        <form onSubmit={handleAddPlayer} className="card">
          <h3>Add Player</h3>
          <label>
            Username
            <input
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
            />
          </label>
          <label>
            Position (optional)
            <select
              value={formData.position}
              onChange={(e) =>
                setFormData({ ...formData, position: e.target.value as Position })
              }
            >
              {positions.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </label>
          <label>
            Rating (50-100)
            <input
              type="number"
              min={50}
              max={100}
              value={formData.rating}
              onChange={(e) =>
                setFormData({ ...formData, rating: parseInt(e.target.value) || 70 })
              }
            />
          </label>
          <button type="submit">Add</button>
        </form>
      )}

      {players.length === 0 ? (
        <p>No players yet. Add one to get started!</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Position</th>
              <th>Rating</th>
              <th>Team</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {players.map((player) => (
              <tr key={player.id}>
                <td>{player.username}</td>
                <td>{player.position}</td>
                <td>{player.rating}</td>
                <td>{player.team_name || "—"}</td>
                <td className="actions">
                  <button
                    onClick={() => {
                      setEditingId(player.id);
                      setFormData({
                        username: player.username,
                        position: player.position,
                        rating: player.rating,
                      });
                    }}
                  >
                    Edit
                  </button>
                  <button onClick={() => handleDeletePlayer(player.id)} className="danger">
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {editingId && (
        <form onSubmit={(e) => handleUpdatePlayer(editingId, e)} className="card">
          <h3>Edit Player</h3>
          <label>
            Position
            <select
              value={formData.position}
              onChange={(e) =>
                setFormData({ ...formData, position: e.target.value as Position })
              }
            >
              {positions.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </label>
          <label>
            Rating (50-100)
            <input
              type="number"
              min={50}
              max={100}
              value={formData.rating}
              onChange={(e) =>
                setFormData({ ...formData, rating: parseInt(e.target.value) || 70 })
              }
            />
          </label>
          <div className="button-group">
            <button type="submit">Save</button>
            <button
              type="button"
              onClick={() => {
                setEditingId(null);
                setFormData({ username: "", position: "Striker", rating: 70 });
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
