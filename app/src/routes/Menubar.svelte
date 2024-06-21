<script lang="ts">
	import * as Menubar from '$lib/components/ui/menubar';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
	import { page } from '$app/stores';
	import { Button } from '$lib/components/ui/button';
	import UserIcon from 'lucide-svelte/icons/user';
	import { uploadingStateStore } from '$lib';
	import Spinner from '$lib/components/Spinner.svelte';
	import { InfoButton } from '$lib/components/InfoButton';
	import { menubarOverrides } from '$lib/components/ui/menubar/overrides';

	$: segments = $page.url.pathname.split('/');

	// now, if the segment looks like an internal ID of the session
	// just replace it with the actual name of the session, and in the snippet
	let overrideSegments: { [id: string]: string } = {};
	menubarOverrides.subscribe((value) => (overrideSegments = value));

	// Workaround for https://github.com/sveltejs/eslint-plugin-svelte/issues/652
	page;

	let loading: boolean = false;
	$: isInSession = segments.length > 2 && segments[1] === 'session';

	uploadingStateStore.subscribe((val) => (loading = val));
</script>

<Menubar.Root class="flex h-12 justify-center bg-secondary py-0 text-secondary-foreground">
	<Menubar.Menu>
		<div class="flex-1 pl-4">
			{@render breadcrumbs()}
		</div>

		<div>
			Spectral

			<!-- TODO: Add logo -->
		</div>

		<div class="flex h-full flex-1 items-center justify-end text-muted-foreground">
			{#if loading}
				<Spinner />
			{/if}
			{#if isInSession}
				<InfoButton />
			{/if}
			<Button href="/profile" variant="ghost">
				<div class="pr-3">Profile</div>
				<UserIcon></UserIcon>
			</Button>
		</div>
	</Menubar.Menu>
</Menubar.Root>

{#snippet breadcrumbs()}
	<Breadcrumb.Root>
		<Breadcrumb.List>
			<Breadcrumb.Item>
				<Breadcrumb.Link href="/">home</Breadcrumb.Link>
			</Breadcrumb.Item>

			{#each segments.slice(1) as pathSegment, i}
				{@const href = segments.slice(0, i + 2).join('/')}
				<Breadcrumb.Separator></Breadcrumb.Separator>

				<Breadcrumb.Item>
					<Breadcrumb.Link {href}>{overrideSegments[pathSegment] || pathSegment}</Breadcrumb.Link>
				</Breadcrumb.Item>
			{/each}
		</Breadcrumb.List>
	</Breadcrumb.Root>
{/snippet}
