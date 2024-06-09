<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button } from '$lib/components/ui/button';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<svelte:head>
	<title>Your profile</title>
</svelte:head>

<main class="mx-auto max-w-xl py-8">
	<h1 class="text-5xl">
		Hello, <strong>{data.user.username}</strong>!
	</h1>
	<p class="text-sm text-muted-foreground">
		{data.user.email}
	</p>
	<p class="text-sm text-muted-foreground">
		{data.user.id}
	</p>

	<p>
		You have uploaded {data.fileCount} files and have {data.sessionCount} sessions.
	</p>

	<form class="pt-2" method="post" use:enhance action="?/logout">
		<Button type="submit" variant="destructive">Log out</Button>
	</form>
</main>
