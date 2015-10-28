function [ numOfEdgesMeeting ] = getNumOfEdgesMeeting( neighbour_matrix, orig_vertex_id_matlab )
%GETNUMOFEDGESMEETING Summary of this function goes here
%   Detailed explanation goes here

numOfEdgesMeeting = sum(neighbour_matrix(orig_vertex_id_matlab,:,1) ~= -1);


end

