name: "Bug Report"
description: "Report a bug to help us improve"
title: "[BUG] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug! Please fill out the form below.

  - type: textarea
    id: description
    attributes:
      label: "Description"
      description: "Clear description of the bug"
      placeholder: "What happened?"
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: "Steps to Reproduce"
      description: "Steps to reproduce the behavior"
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: "Expected Behavior"
      description: "What should happen?"
      placeholder: "Expected behavior..."
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: "Actual Behavior"
      description: "What actually happens?"
      placeholder: "Actual behavior..."
    validations:
      required: true

  - type: input
    id: environment
    attributes:
      label: "Environment"
      description: "OS, Python version, etc."
      placeholder: "Windows 11, Python 3.11, Chrome"

  - type: textarea
    id: screenshots
    attributes:
      label: "Screenshots"
      description: "Add screenshots if applicable"

  - type: checkboxes
    id: checklist
    attributes:
      label: "Checklist"
      options:
        - label: "I have searched existing issues"
          required: true
        - label: "I am using the latest version"
          required: false
        - label: "I have provided all necessary information"
          required: true
