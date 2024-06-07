<script lang="ts">
	import RecorderSingle from './RecorderSingle.svelte';
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PromptResponse } from './recorder';
	import { Button } from '$lib/components/ui/button';
	import { todo } from '$lib/utils';

	export let prompts: PromptResponse[];
	export let recording = false;

	let selectedIndex: number = 0;

	$: console.log({ selectedIndex });

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'ArrowRight') {
			next();
		} else if (event.key === 'ArrowLeft') {
			previous();
		}
	}

	const next = () =>
		!recording && (selectedIndex = Math.min(prompts.length - 1, selectedIndex + 1));
	const previous = () => !recording && (selectedIndex = Math.max(0, selectedIndex - 1));

	const windowSize = 2;
	$: center = Math.min(Math.max(windowSize, selectedIndex), prompts.length - windowSize);
</script>

<svelte:window on:keydown={handleKeydown} />

<main class="h-full">
	<Resizable.PaneGroup class="flex h-full" direction="horizontal">
		<Resizable.Pane
			class="z-30 flex flex-col gap-2 bg-secondary/50 p-4 pt-2 text-secondary-foreground"
			defaultSize={20}
		>
			<p class="text-muted-foreground">For session &lt;session-id&gt</p>

			<p>
				You have recorded {prompts.filter((prompt) => prompt.recordings.length > 0)
					.length}/{prompts.length} prompts
			</p>

			<div class="flex-1"></div>

			<Button on:click={() => todo()}>Export recording to session</Button>
			<Button on:click={() => todo()} variant="outline">Save files to disk</Button>
		</Resizable.Pane>

		<Resizable.Handle withHandle></Resizable.Handle>

		<Resizable.Pane class="relative mx-auto h-full py-4">
			{#each prompts
				.map((prompt, i) => ({ prompt, i }))
				.slice(center - windowSize, center + windowSize + 1) as { prompt, i } (prompt.id)}
				<section
					class:unselected={i !== selectedIndex}
					style:--index={i}
					style:--selected-index={selectedIndex}
					class="absolute z-20 h-[calc(100%-theme(space.8))] w-full overflow-y-scroll text-balance rounded p-4 text-center text-secondary-foreground transition"
				>
					<RecorderSingle
						bind:prompt={prompts[i]}
						bind:recording
						focused={i === selectedIndex}
						onNext={next}
						onPrevious={previous}
					/>
				</section>
			{/each}
		</Resizable.Pane>
	</Resizable.PaneGroup>
</main>

<style lang="postcss">
	section {
		--gap: calc(theme(maxWidth.xl) + theme(space.8));
		transform: translateX(calc((var(--index) - var(--selected-index)) * var(--gap))) var(--scale);

		transition-timing-function: cubic-bezier(0.2, 1, 0.22, 1);
		transition-duration: 1.2s;
	}

	.unselected {
		--scale: scale(0.95);
		@apply pointer-events-none z-0 opacity-50;
	}
</style>
