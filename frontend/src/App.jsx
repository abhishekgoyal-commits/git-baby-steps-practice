import { useEffect, useState } from 'react';

function App() {
	const [health, setHealth] = useState({ status: 'checking' });

	useEffect(() => {
		fetch('/api/health')
			.then((response) => response.json())
			.then(setHealth)
			.catch(() => setHealth({ status: 'unavailable' }));
	}, []);

	return (
		<main className="dashboard-shell">
			<section className="hero">
				<p className="eyebrow">Jira delivery intelligence</p>
				<h1>Sprint command center</h1>
				<p className="lede">A runnable foundation for sprint health, workload, and delivery risk.</p>
				<div className={`service-status service-status--${health.status}`}>
					<span aria-hidden="true" />
					Backend {health.status}
				</div>
			</section>

			<section className="metrics" aria-label="Dashboard preview">
				<article>
					<span>Completion</span>
					<strong>--</strong>
					<small>Jira integration pending</small>
				</article>
				<article>
					<span>Remaining points</span>
					<strong>--</strong>
					<small>Active sprint not configured</small>
				</article>
				<article>
					<span>Delivery risks</span>
					<strong>--</strong>
					<small>Waiting for source data</small>
				</article>
			</section>
		</main>
	);
}

export default App;
