<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PaneGroupAPI } from 'paneforge';

	let {
		captions,
		duration
	}: {
		captions: Caption[];
		duration: number;
	} = $props();

	let paneGroup: PaneGroupAPI | undefined = $state(undefined);
	let handleElementList: HTMLElement[] = $state([]);
	let currentlyHeldButton: HTMLElement | null = null;

	$effect(() => {
		if (handleElementList === null) {
			return;
		}

		for (const [index, element] of handleElementList.entries()) {
			if (element === null) continue;

			element.onmousedown = (event: MouseEvent) => {
				if (event.altKey) {
					// index and index + 1 should merge
					let newEnd = captions[index + 1].end;
					captions.splice(index + 1, 1);
					captions[index].end = newEnd;
				} else {
					currentlyHeldButton = element;
				}
			};
		}
	});

	type Caption = {
		start: number;
		end: number;
		value: string;
	};

	function onClick(event: MouseEvent, caption: Caption) {
		if (!event.altKey) {
			return;
		}

		let boundingBox = (event.target! as HTMLElement).getBoundingClientRect();
		let percentage = (event.x - boundingBox.left) / boundingBox.width;
		let oldEnd = caption.end;
		let ind = captions.indexOf(caption);

		caption.end = caption.start + (caption.end - caption.start) * percentage;

		let newCaption: Caption = {
			start: caption.end,
			end: oldEnd,
			value: ''
		};

		captions = [...captions.slice(0, ind + 1), newCaption, ...captions.slice(ind + 1)];
	}
</script>

<div class="flex w-full flex-row items-center gap-4">
	<Resizable.PaneGroup direction="horizontal" class="w-full" bind:paneGroup>
		{#if duration !== undefined}
			{#each captions as caption, i ([caption.start, caption.end])}
				<Resizable.Pane class="w-full" defaultSize={(caption.start - caption.end) / duration}>
					<span
						role="button"
						tabindex="0"
						class="flex h-full w-full content-center justify-center overflow-hidden rounded-none bg-secondary text-secondary-foreground"
						onclick={(event: MouseEvent) => onClick(event, caption)}
						ondblclick={(event: MouseEvent) => {
							const element = (event.target! as HTMLElement);
							element.contentEditable = 'true';
						}}
						onfocusout={(event: FocusEvent) => {
							const element = event.target! as HTMLElement;
							element.contentEditable = 'false';
							caption.value = element.textContent ?? '';
						}}
						onkeydown={(event: KeyboardEvent) => {
							const element = event.target! as HTMLElement;

							if (!element.isContentEditable) {
								return;
							}

							if (event.key === 'Enter') {
								element.contentEditable = 'false';
								caption.value = element.textContent ?? '';
							} else if (event.key === 'Escape') {
								element.contentEditable = 'false';
								element.textContent = caption.value;
							}
						}}
						>{caption.value}</span
					>
				</Resizable.Pane>

				{#if caption !== captions[captions.length - 1]}
					<Resizable.Handle bind:el={handleElementList[i]}></Resizable.Handle>
				{/if}
			{/each}
		{/if}
	</Resizable.PaneGroup>
</div>

<svelte:window
	on:mouseup={(e) => {
		if (currentlyHeldButton === null || paneGroup === undefined) {
			return;
		}

		e.preventDefault();

		let layout = paneGroup.getLayout();
		let prevEnd = 0;

		for (let i = 0; i < layout.length; i++) {
			captions[i].start = prevEnd;
			captions[i].end = prevEnd + duration * (layout[i] / 100);
			prevEnd = captions[i].end;
		}

		currentlyHeldButton = null;

		return;
	}}
/>
