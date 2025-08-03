// Polyfills for browser compatibility
import { Buffer } from 'buffer';

// Make Buffer available globally
window.Buffer = Buffer;

// Provide process.env for gray-matter
window.process = {
  env: {
    NODE_ENV: 'production'
  }
}; 