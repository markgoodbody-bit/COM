import { Router, Request, Response, NextFunction } from 'express';

/**
 * GET /api/active-coordination
 *
 * Returns the current status of the active coordination subsystem.
 * The payload follows the shape defined in `ActiveCoordinationStatus`.
 */
export interface ActiveCoordinationStatus {
  /** ISO timestamp of the last coordination cycle */
  lastCycle: string;
  /** Whether the coordination loop is currently running */
  isRunning: boolean;
  /** Number of active threads being coordinated */
  activeThreadCount: number;
  /** Optional message for human operators */
  message?: string;
}

/**
 * Simulated in‑memory store for the coordination status.
 * In a real deployment this would be backed by a DB or a state‑machine service.
 */
let status: ActiveCoordinationStatus = {
  lastCycle: new Date().toISOString(),
  isRunning: true,
  activeThreadCount: 0,
  message: 'System initialized',
};

/**
 * Helper to safely update the status object.
 */
function updateStatus(updater: (s: ActiveCoordinationStatus) => void) {
  const newStatus = { ...status };
  updater(newStatus);
  status = newStatus;
}

/**
 * Express router exposing the coordination endpoint.
 */
const router = Router();

/**
 * GET handler – returns the current status.
 */
router.get(
  '/',
  async (_req: Request, res: Response<ActiveCoordinationStatus>, _next: NextFunction) => {
    // In a real system we might compute the status lazily.
    res.json(status);
  },
);

/**
 * POST handler – allows a privileged client to push a status update.
 * The payload must conform to `Partial<ActiveCoordinationStatus>`.
 * Authentication/authorization is out of scope for this scaffold.
 */
router.post(
  '/',
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const payload: Partial<ActiveCoordinationStatus> = req.body;
      if (Object.keys(payload).length === 0) {
        return res.status(400).json({ error: 'Empty payload' });
      }

      updateStatus((s) => {
        if (payload.lastCycle) s.lastCycle = payload.lastCycle;
        if (typeof payload.isRunning === 'boolean') s.isRunning = payload.isRunning;
        if (typeof payload.activeThreadCount === 'number')
          s.activeThreadCount = payload.activeThreadCount;
        if (payload.message !== undefined) s.message = payload.message;
      });

      res.status(200).json(status);
    } catch (err) {
      next(err);
    }
  },
);

export default router;
