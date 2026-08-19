import cors from 'cors';
import express from 'express';

const app = express();
const port = Number(process.env.PORT || 3001);

app.use(cors());
app.use(express.json());

app.get('/api/health', (_request, response) => {
	response.json({
		status: 'ok',
		service: 'backend',
		timestamp: new Date().toISOString()
	});
});

app.get('/api/dashboard', (_request, response) => {
	response.json({
		sprint: {
			name: 'Active sprint',
			status: 'scaffold'
		},
		metrics: {
			completionPercentage: null,
			plannedStoryPoints: 0,
			completedStoryPoints: 0,
			remainingStoryPoints: 0,
			blockedIssues: 0,
			overdueIssues: 0
		},
		refresh: {
			status: 'unavailable',
			message: 'Jira integration is not configured yet.'
		}
	});
});

app.listen(port, () => {
	console.log(`Backend listening on http://localhost:${port}`);
});
