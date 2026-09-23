import express, { Request, Response, NextFunction } from 'express';
import helmet from 'helmet';
import morgan from 'morgan';
import activeCoordinationRouter from './routes/activeCoordination';
import bodyParser from 'body-parser';

// Create Express application
const app = express();

// Middleware stack
app.use(helmet()); // Security headers
app.use(morgan('combined')); // Request logging
app.use(bodyParser.json()); // Parse JSON bodies

// Health‑check endpoint
app.get('/healthz', (_req: Request, res: Response) => {
  res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Mount the active coordination API under /api/active-coordination
app.use('/api/active-coordination', activeCoordinationRouter);

// Global error handler – returns JSON error payloads
app.use((err: unknown, _req: Request, res: Response, _next: NextFunction) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal Server Error' });
});

// Start the server if this module is the entry point
if (require.main === module) {
  const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;
  app.listen(PORT, () => {
    console.info(`🚀 Server listening on http://localhost:${PORT}`);
  });
}

// Export the app for testing purposes
export default app;
