<script lang="ts">
	import UploadPrompt from './UploadPrompt.svelte';
	import Recorder from './Recorder.svelte';
	import type { PromptResponse } from './recorder';
	import { beforeNavigate, onNavigate } from '$app/navigation';

	let state: {
		promptName: string;
		prompts: PromptResponse[];
		participantId: string;
		participantNote: string;
	} | null = null;

	let stopRecording = false;

	onNavigate(() => {
		stopRecording = false;
	});

	$: dirty = state !== null && state.prompts.some((prompt) => prompt.recordings.length > 0);

	beforeNavigate(async ({ cancel }) => {
		if (dirty) {
			if (!confirm('Warning: If you leave the page, your recordings will be lost')) {
				cancel();
				return;
			}
		}
		stopRecording = true;
		await delay(1000); // sometimes the stopRecording isn't propegated correctly in time. This ensures it propagates
		state = null;
	});

	const delay = (delayInms: number) => {
		return new Promise((resolve) => setTimeout(resolve, delayInms));
	};
</script>

<svelte:head>
	<title>Recorder</title>
</svelte:head>

{#if state === null}
	<UploadPrompt
		onFormSubmit={(participantId, participantNote, { fileName, prompts }) => {
			state = {
				participantId,
				participantNote,
				promptName: fileName,
				prompts: prompts.map((prompt) => ({ ...prompt, recordings: [] }))
			};
		}}
	/>
{:else}
	<Recorder
		{stopRecording}
		participantId={state.participantId}
		participantNote={state.participantNote}
		bind:promptName={state.promptName}
		bind:prompts={state.prompts}
	/>
{/if}
