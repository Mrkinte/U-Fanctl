<script setup lang="ts">
import { useMessage } from "naive-ui";
import { setMessageInstance } from "../utils/message.ts";

const message = useMessage();
setMessageInstance(message);
</script>

<template></template>

<style scoped></style>
