<script lang="ts">
	import { buttonVariants } from '$lib/components/ui/button';
	import type { PageData } from './$types';
	import SessionCard from './SessionCard.svelte';
	import { cn } from '$lib/utils';

	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';

	import PlusIcon from 'lucide-svelte/icons/plus';
	import { enhance } from '$app/forms';

	export let data: PageData;
</script>

<Dialog.Root>
	<main class="mx-auto w-fit px-4 py-8">
		<h1 class="text-3xl font-bold">Your sessions</h1>
		<ul class="grid grid-cols-3 gap-4 py-4">
			<li>
				<Dialog.Trigger class={cn(buttonVariants(), 'h-full w-full text-xl font-bold')}>
					<PlusIcon class="mx-12 my-8 h-16 w-16" strokeWidth={1.5}></PlusIcon>
				</Dialog.Trigger>
			</li>

			{#each data.sessions as session}
				<li>
					<SessionCard {session}></SessionCard>
				</li>
			{/each}
		</ul>
	</main>

	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title class="text-3xl">Enter new session name</Dialog.Title>
			<Dialog.Description>
				<form method="POST" use:enhance>
					<Label>
						<Input type="text" name="sessionName" minlength={1} required></Input>
					</Label>
				</form>
			</Dialog.Description>
		</Dialog.Header>
	</Dialog.Content>
</Dialog.Root>
