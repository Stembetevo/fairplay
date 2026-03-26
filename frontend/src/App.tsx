import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { AppLayout } from "./components/AppLayout";

// Auth pages
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";

// Feature pages
import { PlayersPage } from "./pages/PlayersPage";
import { TeamGeneratePage } from "./pages/TeamGeneratePage";
import { TeamsPage } from "./pages/TeamsPage";
import { TeamHistoryPage } from "./pages/TeamHistoryPage";
import { MatchesPage } from "./pages/MatchesPage";
import { MatchCreatePage } from "./pages/MatchCreatePage";
import { MatchDetailPage } from "./pages/MatchDetailPage";
import { MyHistoryPage } from "./pages/MyHistoryPage";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<AppLayout />}>
              <Route path="/players" element={<PlayersPage />} />
              <Route path="/teams/generate" element={<TeamGeneratePage />} />
              <Route path="/teams" element={<TeamsPage />} />
              <Route path="/teams/:teamId/history" element={<TeamHistoryPage />} />
              <Route path="/matches" element={<MatchesPage />} />
              <Route path="/matches/new" element={<MatchCreatePage />} />
              <Route path="/matches/:matchId" element={<MatchDetailPage />} />
              <Route path="/history" element={<MyHistoryPage />} />
            </Route>
          </Route>

          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/players" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
