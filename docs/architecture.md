# Finova Architecture

## Core principle
**Deterministic engine decides what happened. AI reasons about why it happened. Policy engine decides what the system is allowed to do.**

## Data flow
Synthetic source records → validation → normalization → reconciliation → exception detection → risk scoring → historical exception retrieval → AI investigation → policy evaluation → human review → audit.

## Human control
Financial actions are never delegated to the LLM. High-risk, duplicate, and policy-triggered exceptions require human review.
