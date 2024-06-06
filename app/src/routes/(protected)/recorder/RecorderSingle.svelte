<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { ArrowLeftIcon, ArrowRightIcon, MicIcon, TrashIcon } from 'lucide-svelte';
	import Camera from './Camera.svelte';
	import { Textarea } from '$lib/components/ui/textarea';
	import type { PromptResponse } from './recorder';
	import { fly } from 'svelte/transition';

	export let prompt: PromptResponse;
	export let focused: boolean;
	export let recording: boolean = false;

	/**
	 * Called when requesting to go to previous prompt
	 */
	export let onPrevious: () => void = () => {};

	/**
	 * Called when requesting to go to next prompt
	 */
	export let onNext: () => void = () => {};

	/**
	 * The index of the recording that is currently being previewed.
	 */
	let previewingIndex: number | null = null;
	let previewing = previewingIndex !== null ? prompt.recordings[previewingIndex] : null;

	let cameraComponent: Camera;

	function toggleRecording() {
		cameraComponent.toggleRecording();
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'r') {
			if (focused) {
				cameraComponent.toggleRecording();
			}
		}
	}
</script>

<svelte:window on:keydown={handleKeydown} />

<div>
	<div class="pb-2">
		<h1 class="text-5xl">{prompt.content}</h1>
		<p class="text-muted-foreground">{prompt.id}</p>
	</div>

	<Camera
		class="delay-50 mb-4 transition duration-200 {focused ? '' : 'opacity-0'}"
		bind:this={cameraComponent}
		bind:recording
		previewing={previewing?.blob}
		onStopRecording={(blob) => {
			prompt.recordings.push({ blob, note: '' });
			prompt = prompt;
		}}
	/>

	<div>
		<div class="flex h-14 w-full justify-end gap-2">
			<Button
				class="relative mb-2 h-full w-full bg-red-800 bg-opacity-80 p-0 text-white shadow hover:bg-red-700"
				on:click={toggleRecording}
			>
				<MicIcon class="h-5 w-5 transition"></MicIcon>
				<span class="pl-2 transition"> {recording ? 'Stop recording' : 'Record'} </span>
			</Button>

			<Button on:click={onPrevious} class="h-full">
				<ArrowLeftIcon />
			</Button>

			<Button on:click={onNext} class="h-full">
				<ArrowRightIcon />
			</Button>
		</div>
	</div>

	<div class="flex h-full">
		<ul class="flex flex-1 flex-col gap-1 overflow-y-scroll pt-4">
			{#each prompt.recordings as recording, i (recording)}
				<li transition:fly={{ x: -20 }} class="flex items-center gap-1">
					<Button
						class="w-full transition {previewingIndex === i ? 'opacity-50' : ''}"
						on:click={() => {
							if (previewingIndex === i) {
								previewingIndex = null;
							} else {
								previewingIndex = i;
							}
						}}
					>
						Take {i + 1}
					</Button>

					<Button
						variant="destructive"
						class="h-fit p-1"
						on:click={() => {
							prompt.recordings = prompt.recordings.toSpliced(i, 1);
							if (previewingIndex === i) {
								previewingIndex = null;
							} else if (previewingIndex !== null && previewingIndex > i) {
								previewingIndex -= 1;
							}
						}}
					>
						<TrashIcon class="w-4" />
					</Button>
				</li>
			{/each}
		</ul>

		{#if previewing}
			<div class="m-4 h-full flex-1 rounded bg-background p-2">
				Notes
				<Textarea bind:value={previewing.note}></Textarea>
			</div>
		{/if}
	</div>
</div>
