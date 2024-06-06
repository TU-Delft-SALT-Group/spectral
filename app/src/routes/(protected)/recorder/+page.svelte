<script lang="ts">
	import UploadPrompt from './UploadPrompt.svelte';
	import Recorder from './Recorder.svelte';
	import type { PromptResponse } from './recorder';
	import { browser } from '$app/environment';

	let state: {
		promptName: string;
		prompts: PromptResponse[];
	} | null = null;

	// TODO: Remove this
	// $: browser && localStorage.setItem('recording-state', JSON.stringify(state))
	state = browser ? JSON.parse(localStorage.getItem('recording-state') || 'null') : null;
</script>

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
	<Recorder bind:prompts={state.prompts} />
{/if}
