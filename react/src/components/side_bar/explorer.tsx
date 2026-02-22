import { Box } from "@mui/material";
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import type { Tree } from '@/src/lib/types';

import TreeHandler from '@/src/lib/tree_handler';


function Explorer(props: { tree: Tree, nodeId: string }) {
  const navigate = useNavigate();
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const treeHandler = new TreeHandler(props.tree);
  const parents = treeHandler.getParentNodeIds(props.nodeId);
  const displayedExpanded = [
    ...new Set([props.tree.node_id, ...expandedItems, ...parents]),
  ];

  function getItemId(item: Tree) {
    return item.node_id;
  }

  return (
    <>
      <Box >
        <RichTreeView
          sx={{}}
          items={[props.tree]}
          getItemId={getItemId}
          onItemClick={(_, nodeId) => {
            navigate(`/node/${nodeId}`);
          }}
          selectedItems={props.nodeId}
          expandedItems={displayedExpanded}
          onExpandedItemsChange={(_, ids) => setExpandedItems(ids)}
        />
      </Box>
    </>
  );
};

export default Explorer;
