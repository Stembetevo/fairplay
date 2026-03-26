import { apiRequest } from "./client";
import type { MyHistoryResponse } from "../types";

export function getMyHistory(): Promise<MyHistoryResponse> {
  return apiRequest<MyHistoryResponse>("/history/me");
}
