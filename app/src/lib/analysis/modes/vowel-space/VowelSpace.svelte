<script lang="ts">
	import { getPaletteColor } from '$lib/color';
	import used, { unwrap } from '$lib/utils';
	import type { ModeComponentProps } from '..';
	import * as d3 from 'd3';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { Label } from '$lib/components/ui/label';

	export let fileData: ModeComponentProps<'vowel-space'>['fileData'];
	export let modeState: ModeComponentProps<'vowel-space'>['modeState'];

	used(modeState);

	let container: HTMLDivElement;

	function d3Action(node: Node) {
		const foreground = window && window.getComputedStyle(container).getPropertyValue('color');
		// const background = window && window.getComputedStyle(container).getPropertyValue('background-color')

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
			.domain([2800, 200])
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

		const legend = svg.append('g').attr('class', 'legend').style('transition', 'all 0.2s ease');

		for (let i = 0; i < fileData.length; i++) {
			const {
				computedData: { f1, f2 },
				fileState: { filename }
			} = fileData[i];
			const color = getPaletteColor(i);

			svg
				.append('circle')
				.attr('cx', x(f2 - f1))
				.attr('cy', y(f1))
				.attr('r', 10)
				.attr('fill', color)
				.attr('cursor', 'pointer')
				.attr('title', filename);

			svg
				.append('text')
				.attr('x', x(f2 - f1) + 10)
				.attr('y', y(f1) + 17)
				.text(filename)
				.attr('fill', foreground)
				.attr('font-size', '0.9rem')
				.attr('alignment-baseline', 'middle');

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
				.text(filename)
				.attr('fill', foreground)
				.attr('font-size', '1rem')
				.attr('alignment-baseline', 'middle');
		}

		node.appendChild(unwrap(svg.node()));
	}

	$: d3.select('.legend').style('opacity', modeState.showLegend ? 1 : 0);
</script>

<section class="grid h-full w-full grid-rows-[auto,1fr]">
	<div class="w-full p-2">
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
</section>
