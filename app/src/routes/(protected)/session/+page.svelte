<script lang="ts">
	import { buttonVariants } from '$lib/components/ui/button';
	import type { PageData } from './$types';
	import SessionCard from './SessionCard.svelte';
	import { cn } from '$lib/utils';

	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';

	import PlusIcon from 'lucide-svelte/icons/plus';
	import { enhance } from '$app/forms';

	import { toast } from 'svelte-sonner';
	import { Toaster } from '$lib/components/ui/sonner';

	let importingSession: boolean = false;
	let openContextMenus: boolean[] = [];

	function closeAllContextMenus() {
		for (let i = 0; i < openContextMenus.length; i++) {
			openContextMenus[i] = false;
		}
	}

	async function handleFileUpload(event: Event) {
		importingSession = true;
		if (!(event.target instanceof HTMLInputElement)) {
			importingSession = false;
			toast.error('session import was unsuccessful', {
				description:
					'This is most likely due to an error on the website, please contact the developers'
			});
			return;
		}

		const { target: input } = event;

		if (input.files === null || input.files.length != 1) {
			toast.error('session import was unsuccessful', {
				description: 'You must upload 1 file'
			});
			importingSession = false;
			return;
		}

		const file = input.files[0];

		if (file.type !== 'application/json') {
			toast.error('session import was unsuccessful', {
				description: 'The file has to be in the JSON format'
			});
			importingSession = false;
			return;
		}

		const sessionJSON = await readAsJSONtext(file);

		await fetch('?/importSession', {
			method: 'POST',
			body: sessionJSON
		}).then(async (response) => {
			const responseJSON = await response.json();
			if (responseJSON.status === 301) {
				window.location.href = `/${responseJSON.location}`;
			} else {
				toast.error('session import was unsuccessful', {
					description:
						'This is most likely because the file format is not correct or because of internet issues'
				});
			}
		});
		importingSession = false;
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

			{#each data.sessions as session, i}
				<li>
					<SessionCard
						{session}
						{closeAllContextMenus}
						bind:isContextMenuOpen={openContextMenus[i]}
						onDeleteSession={() => {
							data.sessions = data.sessions.filter((s) => s.id !== session.id);
						}}
					></SessionCard>
				</li>
			{/each}
		</ul>
	</main>

	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title class="text-3xl">Enter new session name</Dialog.Title>
			<Dialog.Description>
				<form action="?/createSession" method="POST" use:enhance>
					<Input disabled={importingSession} type="text" name="sessionName" minlength={1} required
					></Input>
				</form>
			</Dialog.Description>
			<Dialog.Title class="text-3xl">Or Import a session</Dialog.Title>
			<Dialog.Description>
				<Input
					name="file"
					type="file"
					accept="application/json"
					disabled={importingSession}
					class={cn(buttonVariants({ variant: 'ghost' }))}
					on:change={(event) => handleFileUpload(event)}
				/>
			</Dialog.Description>
		</Dialog.Header>
	</Dialog.Content>
</Dialog.Root>

<Toaster />
