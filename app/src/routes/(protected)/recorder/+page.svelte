<script lang="ts">
	import UploadPrompt from './UploadPrompt.svelte';
	import Recorder from './Recorder.svelte';
	import type { PromptResponse } from './recorder';
	import { beforeNavigate } from '$app/navigation';

	let state: {
		promptName: string;
		prompts: PromptResponse[];
	} | null = null;

	$: dirty = state !== null && state.prompts.some((prompt) => prompt.recordings.length > 0);

	beforeNavigate(({ cancel }) => {
		if (dirty) {
			if (!confirm('Warning: If you leave the page, your recordings will be lost')) {
				cancel();
			}
		}
	});
</script>

<svelte:head>
	<title>Recorder</title>
</svelte:head>

{#if state === null}
	<UploadPrompt
		onPromptUpload={({ filename, prompts }) => {
			state = {
				promptName: filename,
				prompts: prompts.map((prompt) => ({ ...prompt, recordings: [] }))
			};
		}}
	/>
{:else}
	<Recorder bind:promptName={state.promptName} bind:prompts={state.prompts} />
{/if}
