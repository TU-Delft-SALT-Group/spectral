<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import type { Transcriptions } from '../file-state';

	let { transcriptions, width }: { transcriptions: Transcriptions; width: number | undefined } =
		$props();

	function onClick(event: MouseEvent) {
		if (width === undefined) {
			return;
		}

		event.stopImmediatePropagation(); // to stop the cursor from moving
		let element = event.target! as HTMLElement;

		let lmao = element.getBoundingClientRect();
		let percent = (event.x - lmao.left) / lmao.width;

		let currentWidth = (100 * element.clientWidth) / width;

		let newButton = document.createElement('button');
		newButton.style.width = `${currentWidth * (1 - percent)}%`;
		newButton.style.height = '100%';
		newButton.innerText = 'test';

		element.style.width = `${currentWidth * percent}%`;
		element.insertAdjacentElement('afterend', newButton);
	}
</script>

<div style:width={`${width}px` ?? '100%'}>
	{#each transcriptions as track}
		<div class="w-auto">
			<Button class="w-full overflow-hidden bg-black text-white" variant="outline" onclick={onClick}
				>{track}</Button
			>
		</div>
	{/each}
</div>
