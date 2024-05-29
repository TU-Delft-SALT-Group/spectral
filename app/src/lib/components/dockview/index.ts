import used from '$lib/utils';
import type {
	DockviewApi,
	DockviewGroupPanel,
	GroupPanelPartInitParameters,
	IContentRenderer,
	IGroupHeaderProps,
	IHeaderActionsRenderer,
	ITabRenderer,
	PanelUpdateEvent,
	Parameters
} from 'dockview-core';

import { type SvelteComponent, mount, unmount, type ComponentType } from 'svelte';
import { paneState, type PaneState } from '$lib/analysis/analysis-pane';

abstract class AbstractSvelteRenderer {
	readonly _element: HTMLElement;

	get element() {
		return this._element;
	}

	constructor() {
		this._element = document.createElement('section');
		this.element.className = 'dv-vue-part';
		this.element.style.height = '100%';
	}
}

export class SvelteRenderer<S extends Record<string, unknown>>
	extends AbstractSvelteRenderer
	implements IContentRenderer, ITabRenderer
{
	readonly _component: ComponentType<SvelteComponent<S>>;
	private _instance: ComponentType<SvelteComponent<S>> | undefined;
	private _props: S | undefined;

	constructor(component: ComponentType<SvelteComponent<S>>) {
		super();
		this._component = component;
	}

	init(parameters: GroupPanelPartInitParameters): void {
		this._props = parameters.params as S;

		this._instance = mount(this._component, {
			target: this._element,
			props: this._props
		}) as ComponentType<SvelteComponent<S>>;
	}

	update(event: PanelUpdateEvent<Parameters>): void {
		if (this._instance === undefined) {
			return;
		}

		const params = event.params.params as S;
		this._props = { ...(this._props as S), ...params };
	}

	dispose(): void {
		if (this._instance !== undefined) {
			unmount(this._instance);
		}
	}
}

type TabRequirements = {
	containerApi: DockviewApi;
	defaultProps: { state: PaneState };
};

export class SvelteTabActionRenderer
	extends AbstractSvelteRenderer
	implements IHeaderActionsRenderer
{
	private _params: IGroupHeaderProps | undefined;
	protected _component: ComponentType<SvelteComponent<TabRequirements>>;
	protected _instance: ComponentType<SvelteComponent<TabRequirements>> | undefined;

	constructor(
		component: ComponentType<SvelteComponent<TabRequirements>>,
		group: DockviewGroupPanel
	) {
		super();
		this._component = component;
		used(group);
	}

	init(params: IGroupHeaderProps): void {
		this._params = params;

		const props: TabRequirements = {
			containerApi: this._params.containerApi,
			defaultProps: { state: paneState.parse(undefined) }
		};

		this._instance = mount(this._component, {
			target: this._element,
			props
		}) as ComponentType<SvelteComponent<TabRequirements>>;
	}

	dispose(): void {
		if (this._instance !== undefined) {
			unmount(this._instance);
		}
	}
}
