<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button } from '$lib/components/ui/button';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<main class="mx-auto max-w-xl py-8">
	<h1 class="text-5xl">
		Hello, <strong>{data.user.username}</strong>!
	</h1>
	<p class="text-muted-foreground">
		{data.user.email}
	</p>
	<p class="text-muted-foreground">
		{data.user.id}
	</p>

	<form class="pt-2" method="post" use:enhance action="?/logout">
		<Button type="submit" variant="destructive">Log out</Button>
	</form>
</main>
