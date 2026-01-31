import { Breadcrumbs, Link } from '@mui/material';

import type { Tree } from "@/src/lib/types";

import TreeHandler from '@/src/lib/tree_handler';


function Breadcrumb(props: { node_id: string, tree: Tree }) {
  const tree_handler = new TreeHandler(props.tree);

  let parentNodes: Tree[] = [];
  const parents = tree_handler.getParentNodeIds(props.node_id);
  parentNodes = parents.map((node_id) => tree_handler.getNode(node_id)).filter(node => node != null);
  const this_node = tree_handler.getNode(props.node_id);
  if (this_node) parentNodes.push(this_node);

  return (
    <Breadcrumbs separator="›" aria-label="breadcrumb">
      {parentNodes.map((node, index) => (
        <Link
          key={node.node_id}
          underline="none"
          color={index === parentNodes.length - 1 ? "textDisabled" : "textSecondary"}
          href={index === parentNodes.length - 1 ? undefined : `/main/${node.node_id}`}
          aria-current={index === parentNodes.length - 1 ? "page" : undefined}
        >
          {node.label}
        </Link>
      ))}
    </Breadcrumbs>
  );
}

export default Breadcrumb;
