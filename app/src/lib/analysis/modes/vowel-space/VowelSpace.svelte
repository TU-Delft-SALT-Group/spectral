<script lang="ts">
	import { getPaletteColor } from '$lib/color';
	import { unwrap } from '$lib/utils';
	import type { ModeComponentProps } from '..';
	import * as d3 from 'd3';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { Label } from '$lib/components/ui/label';
	import type { mode } from '..';

	import VowelSpaceSingle from './VowelSpaceSingle.svelte';

	let {
		fileStates = $bindable<mode.FileState<'vowel-space'>[]>(),
		modeState = $bindable<mode.ModeState<'vowel-space'>>(),
		getComputedData
	}: ModeComponentProps<'vowel-space'> = $props();

	let container: HTMLDivElement;
	let tooltip: HTMLDivElement;
	let clientWidth: number = $state(0);
	let clientHeight: number = $state(0);

	function d3Action(node: Node) {
		while (container.hasChildNodes()) {
			container.firstChild?.remove();
		}
		const foreground = window && window.getComputedStyle(container).getPropertyValue('color');

		// Declare the chart dimensions and margins.
		const width = container.clientWidth;
		const height = container.clientHeight;
		const marginTop = 60;
		const marginRight = 100;
		const marginBottom = 20;
		const marginLeft = 20;

		// Declare the x (horizontal position) scale.
		const x = d3
			.scaleLinear()
			.domain([2000, 0])
			.range([marginLeft, width - marginRight]);

		// Declare the y (vertical position) scale.
		const y = d3
			.scaleLinear()
			.domain([2800, 0])
			.range([height - marginBottom, marginTop]);

		// Create the SVG container.
		const svg = d3.create('svg').attr('width', width).attr('height', height);

		// Add the x-axis.
		svg.append('g').attr('transform', `translate(0,${marginTop})`).call(d3.axisTop(x));
		svg
			.append('text')
			.attr('class', 'x label')
			.attr('text-anchor', 'middle')
			.attr('x', width / 2)
			.attr('y', marginTop / 2)
			.style('fill', foreground)
			.style('font-weight', 'bold')
			.text('F2 - F1');

		// Add the y-axis.
		svg
			.append('g')
			.attr('transform', `translate(${width - marginRight},0)`)
			.call(d3.axisRight(y));
		svg
			.append('text')
			.attr('class', 'y label')
			.attr('text-anchor', 'middle')
			.attr('x', width - marginRight / 2)
			.attr('y', height / 2)
			.style('fill', foreground)
			.style('font-weight', 'bold')
			.text('F1');

		const mouseover = function () {
			tooltip.style.opacity = '1';
			d3.select(this).style('stroke', 'black').style('opacity', 1);
		};
		const mousemove = function (
			event: MouseEvent,
			d: {
				name: string;
				color: string;
				f1: number;
				f2: number;
				start: number;
				end: number;
				matchString: string | null;
			}
		) {
			tooltip.innerHTML = `f1: ${d.f1}<br>f2: ${d.f2}<br>match string: ${d.matchString}<br>start: ${d.start}<br>end: ${d.end}`;
			tooltip.style.left = event.layerX + 'px';
			tooltip.style.top = event.layerY + 'px';
		};
		const mouseleave = function () {
			tooltip.style.opacity = '0';
			d3.select(this).style('stroke', 'none').style('opacity', 0.8);
		};

		const legend = svg.append('g').attr('class', 'legend').style('transition', 'all 0.2s ease');
		for (let i = 0; i < fileStates.length; i++) {
			const fileState = fileStates[i];
			const computedData = getComputedData(fileState);
			const color = getPaletteColor(i);
			if (computedData === null) continue;

			const data = computedData.formants.map((formant) => ({
				...formant,
				name: fileState.name,
				color
			}));

			// Bind data and append circles
			const circles = svg
				.selectAll(`circle.formant-${i}`)
				.data(data)
				.enter()
				.append('circle')
				.attr('class', `formant-${i}`)
				.attr('cx', (d) => x(d.f2 - d.f1))
				.attr('cy', (d) => y(d.f1))
				.attr('r', 4)
				.attr('fill', (d) => d.color)
				.attr('cursor', 'pointer')
				.attr('title', (d) => d.name)
				.on('mouseover', mouseover)
				.on('mousemove', mousemove)
				.on('mouseleave', mouseleave);

			// Append texts
			circles
				.enter()
				.append('text')
				.attr('x', (d) => x(d.f2 - d.f1) + 4)
				.attr('y', (d) => y(d.f1) + 11)
				.text((d) => d.matchString)
				.attr('fill', foreground)
				.attr('font-size', '0.9rem')
				.attr('alignment-baseline', 'middle');

			// Add legend entries
			legend
				.append('circle')
				.attr('cx', marginLeft)
				.attr('cy', height - marginBottom - 50 - 30 * i)
				.attr('r', 6)
				.style('fill', color);

			legend
				.append('text')
				.attr('x', marginLeft + 12)
				.attr('y', height - marginBottom - 50 - 30 * i)
				.text(fileState.name)
				.attr('fill', foreground)
				.attr('font-size', '1rem')
				.attr('alignment-baseline', 'middle');
		}

		node.appendChild(unwrap(svg.node() as Node));
	}

	$effect(() => {
		d3.select('.legend').style('opacity', modeState.showLegend ? 1 : 0);
	});

	$effect(() => {
		if (clientWidth && clientHeight) {
			while (container.hasChildNodes()) {
				container.firstChild?.remove();
			}
			d3Action(container);
		}
	});

	$effect(() => {
		if (fileStates) {
			d3Action(container);
		}
	});
</script>

<div class="flex w-full">
	<div class="m-2 w-64 border-r-2 pr-2">
		<h2 class="text-center text-2xl">Match Strings</h2>
		{#each fileStates as fileState, i}
			<VowelSpaceSingle computedData={getComputedData(fileState)} bind:fileState={fileStates[i]}
			></VowelSpaceSingle>
		{/each}
	</div>
	<section
		class="grid min-h-72 w-full min-w-96 grid-rows-[auto,1fr]"
		bind:clientWidth
		bind:clientHeight
	>
		<div class="p-2">
			<div class="flex items-center gap-2">
				<Label
					for="terms"
					class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
					>Show legend</Label
				>
				<Checkbox id="terms" bind:checked={modeState.showLegend} />
			</div>
		</div>
		<div use:d3Action bind:this={container}></div>
		<div class="tooltip" bind:this={tooltip}></div>
	</section>
</div>

<style>
	.tooltip {
		position: absolute;
		opacity: 0;
		background-color: white;
		border: solid 2px;
		border-radius: 5px;
		padding: 5px;
		pointer-events: none;
		transition: opacity 0.2s;
	}
</style>
