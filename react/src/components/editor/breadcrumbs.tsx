import { Breadcrumbs, Link } from '@mui/material';

import type { Tree } from "@/src/lib/types";

import TreeHandler from '@/src/lib/tree_handler';


function Breadcrumb(props: { tree: Tree, nodeId: string }) {
  const treeHandler = new TreeHandler(props.tree);

  let parentNodes: Tree[] = [];
  const parents = treeHandler.getParentNodeIds(props.nodeId);
  parentNodes = parents.map((nodeId) => treeHandler.getNode(nodeId)).filter(node => node != null);
  const thisNode = treeHandler.getNode(props.nodeId);
  if (thisNode) parentNodes.push(thisNode);

  return (
    <Breadcrumbs separator="›" aria-label="breadcrumb">
      {parentNodes.map((node, index) => (
        <Link
          key={node.node_id}
          underline="none"
          color={index === parentNodes.length - 1 ? "textDisabled" : "textSecondary"}
          href={index === parentNodes.length - 1 ? undefined : `/node/${node.node_id}`}
          aria-current={index === parentNodes.length - 1 ? "page" : undefined}
        >
          {node.label}
        </Link>
      ))}
    </Breadcrumbs>
  );
}

export default Breadcrumb;
