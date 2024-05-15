<script>
	import { Button } from '$lib/components/ui/button';
</script>

<main class="mx-auto max-w-xl py-8">
	<h1 class="text-2xl font-bold">Admin dashboard</h1>

	<form method="post" action="?/seedSampleTorgo">
		<Button type="submit">Seed database with TORGO sample data</Button>
	</form>
</main>
