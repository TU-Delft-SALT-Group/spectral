<script lang="ts">
	import { buttonVariants } from '$lib/components/ui/button';
	import type { PageData } from './$types';
	import SessionCard from './SessionCard.svelte';
	import { cn } from '$lib/utils';

	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';

	import PlusIcon from 'lucide-svelte/icons/plus';
	import { enhance } from '$app/forms';

	import * as ContextMenu from '$lib/components/ui/context-menu';

	async function handleFileUpload(event: Event) {
		if (!(event.target instanceof HTMLInputElement)) {
			throw new Error('Event target is not an input element');
		}

		const { target: input } = event;

		if (input.files === null || input.files.length != 1) {
			return;
		}

		const file = input.files[0];

		if (file.type !== 'application/json') {
			return;
		}

		const sessionJSON = await readAsJSONtext(file);

		await fetch('?/importSession', {
			method: 'POST',
			body: sessionJSON
		}).then(async (response) => {
			const responseJSON = await response.json();
			// The page should redirect on a successful import
			if (responseJSON.status === 301) {
				window.location.href = `/${responseJSON.location}`;
			}
		});
	}

	function readAsJSONtext(file: File): Promise<string> {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();
			reader.onload = () => resolve(reader.result as string);
			reader.onerror = reject;
			reader.readAsText(file);
		});
	}

	export let data: PageData;
</script>

<svelte:head>
	<title>Your sessions</title>
</svelte:head>

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
					<ContextMenu.Root closeOnOutsideClick>
						<SessionCard {session}></SessionCard>
					</ContextMenu.Root>
				</li>
			{/each}
		</ul>
	</main>

	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title class="text-3xl">Enter new session name</Dialog.Title>
			<Dialog.Description>
				<form action="?/createSession" method="POST" use:enhance>
					<Input type="text" name="sessionName" minlength={1} required></Input>
				</form>
			</Dialog.Description>
			<Dialog.Title class="text-3xl">Or Import a session</Dialog.Title>
			<Dialog.Description>
				<Input
					name="file"
					type="file"
					accept="application/json"
					class={cn(buttonVariants({ variant: 'ghost' }))}
					on:change={(event) => handleFileUpload(event)}
				/>
			</Dialog.Description>
		</Dialog.Header>
	</Dialog.Content>
</Dialog.Root>
