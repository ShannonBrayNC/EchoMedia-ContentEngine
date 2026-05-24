import React from 'react';
import { toProjectPickerOption } from '../lib/projectRegistry.js';

export default function ProjectPicker({ projects = [], selectedSlug, onSelectProject }) {
  const options = projects.map(toProjectPickerOption);
  const selectedProject = projects.find((project) => project.slug === selectedSlug) || null;

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-950/70 p-4 shadow-lg">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-cyan-300">Project</p>
          <h2 className="text-lg font-semibold text-white">Select story project</h2>
        </div>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">
          {options.length} visible
        </span>
      </div>

      <label className="block text-sm text-slate-300" htmlFor="project-picker">
        Registry project
      </label>
      <select
        id="project-picker"
        className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-900 px-3 py-2 text-white outline-none focus:border-cyan-400"
        value={selectedSlug || ''}
        onChange={(event) => onSelectProject?.(event.target.value)}
      >
        <option value="" disabled>
          Choose a project
        </option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      {selectedProject ? (
        <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900/80 p-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-emerald-500/15 px-2 py-1 text-xs font-medium text-emerald-300">
              {selectedProject.status}
            </span>
            <span className="rounded-full bg-cyan-500/15 px-2 py-1 text-xs font-medium text-cyan-300">
              canon: {selectedProject.canon_state || 'unknown'}
            </span>
          </div>

          <h3 className="mt-3 text-base font-semibold text-white">{selectedProject.title}</h3>
          <p className="mt-1 text-sm text-slate-400">{selectedProject.universe || selectedProject.series}</p>
          <p className="mt-2 font-mono text-xs text-slate-500">{selectedProject.root_path}</p>

          <div className="mt-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Supported generation</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {(selectedProject.supported_generation_types || []).slice(0, 8).map((type) => (
                <span key={type} className="rounded-full bg-slate-800 px-2 py-1 text-xs text-slate-300">
                  {type}
                </span>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <p className="mt-3 text-sm text-slate-500">Select a project to load its artifact paths and generation support.</p>
      )}
    </section>
  );
}
