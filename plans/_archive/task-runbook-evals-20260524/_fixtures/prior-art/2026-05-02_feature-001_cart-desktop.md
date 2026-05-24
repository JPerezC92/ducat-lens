---
identifier: feature-001
module: commerce.cart
surface: desktop-web
shipped: 2026-05-05
---

# Persistent cart across devices — desktop web

## Goal
User adds item to cart on desktop; signs out; signs in on another desktop browser; cart persists.

## Approach
Move cart from localStorage to server-side keyed by user-id. Read cart on session-start. Write debounced (500ms) on every cart mutation. Conflict resolution: last-write-wins per cart-line.

## Implementation steps
1. Schema: `carts` table (user_id PK, items jsonb, updated_at).
2. Backend `/api/cart` GET/PUT endpoints with optimistic concurrency token.
3. Frontend cart slice: rehydrate on session-start; debounced write on mutation.
4. Migration: read existing localStorage carts on first login post-deploy, merge into server cart.

## Validation
20 manual cross-browser scenarios. 1% chaos test on cart write (verifies idempotency).
