/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_CONTENT_ENGINE_API_BASE_URL?: string;
  readonly VITE_EMAS_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
