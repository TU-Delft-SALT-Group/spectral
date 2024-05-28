<script lang="ts">
	import * as Menubar from '$lib/components/ui/menubar';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
	import { page } from '$app/stores';
	import { Button } from '$lib/components/ui/button';
	import UserIcon from 'lucide-svelte/icons/user';

	$: segments = $page.url.pathname.split('/');

	// Workaround for https://github.com/sveltejs/eslint-plugin-svelte/issues/652
	page;
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

		<div class="flex flex-1 justify-end text-muted-foreground">
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
					<Breadcrumb.Link {href}>{pathSegment}</Breadcrumb.Link>
				</Breadcrumb.Item>
			{/each}
		</Breadcrumb.List>
	</Breadcrumb.Root>
{/snippet}
