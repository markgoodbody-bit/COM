import request from 'supertest';
import app from '../src/server';

describe('Active Coordination API', () => {
  it('should return the default status on GET', async () => {
    const response = await request(app).get('/api/active-coordination').expect(200);
    expect(response.body).toMatchObject({
      isRunning: true,
      activeThreadCount: 0,
    });
    expect(typeof response.body.lastCycle).toBe('string');
  });

  it('should accept a valid status update via POST', async () => {
    const payload = {
      isRunning: false,
      activeThreadCount: 5,
      message: 'Paused for maintenance',
    };

    const postRes = await request(app)
      .post('/api/active-coordination')
      .send(payload)
      .set('Content-Type', 'application/json')
      .expect(200);

    expect(postRes.body).toMatchObject({
      isRunning: false,
      activeThreadCount: 5,
      message: 'Paused for maintenance',
    });

    // Verify that a subsequent GET reflects the update
    const getRes = await request(app).get('/api/active-coordination').expect(200);
    expect(getRes.body).toMatchObject({
      isRunning: false,
      activeThreadCount: 5,
      message: 'Paused for maintenance',
    });
  });

  it('should reject an empty POST payload', async () => {
    await request(app)
      .post('/api/active-coordination')
      .send({})
      .set('Content-Type', 'application/json')
      .expect(400)
      .expect(res => {
        expect(res.body).toHaveProperty('error', 'Empty payload');
      });
  });
});
