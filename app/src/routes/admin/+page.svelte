<script lang="ts">
	import type { PageData } from './$types';
	import { Button } from '$lib/components/ui/button';

	export let data: PageData;
</script>

<main class="mx-auto max-w-xl py-8">
	<h1 class="mb-4 text-2xl font-bold">Admin dashboard</h1>

	<section>
		<h2 class="mb-2 text-xl">Database</h2>
		<div>
			<h3 class="text-lg">Table sizes</h3>
			<ul>
				<li>Users: {data.counts.userTable[0].value} rows</li>
				<li>Sessions: {data.counts.sessionTable[0].value} rows</li>
				<li>Files: {data.counts.filesTable[0].value} rows</li>
			</ul>
		</div>

		<form method="post" action="?/seedSampleUser">
			<Button type="submit">Seed database with sample user</Button>
		</form>

		<form method="post" action="?/seedSampleSession">
			<Button type="submit">Seed database with sample session</Button>
		</form>

		<form method="post" action="?/seedSampleTorgo">
			<Button type="submit">Seed database with TORGO sample data</Button>
		</form>

		<form method="post" action="?/deleteAllData">
			<Button type="submit" variant="destructive">Delete all data</Button>
		</form>
	</section>
</main>

<style>
	form {
		margin-top: 0.5rem;
	}
</style>
